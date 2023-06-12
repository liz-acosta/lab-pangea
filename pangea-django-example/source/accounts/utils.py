from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import Message

# Pangea imports
from pangea.config import PangeaConfig
import pangea.exceptions as pe
from pangea.services.vault.models.common import KeyPurpose
from pangea.services.vault.models.symmetric import SymmetricAlgorithm
from pangea.services.vault.vault import Vault
from pangea.services import Audit, Redact
from pangea.utils import str2str_b64

import base64

# Initialize Pangea services
pangea_config = PangeaConfig(domain=settings.PANGEA_DOMAIN)
pangea_vault = Vault(settings.PANGEA_TOKEN, config=pangea_config)
pangea_redact = Redact(settings.PANGEA_TOKEN, config=pangea_config)
pangea_audit = Audit(settings.PANGEA_TOKEN, config=pangea_config)


def send_mail(to, template, context):
    html_content = render_to_string(f'accounts/emails/{template}.html', context)
    text_content = render_to_string(f'accounts/emails/{template}.txt', context)

    msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_activation_email(request, email, code):
    context = {
        'subject': _('Profile activation'),
        'uri': request.build_absolute_uri(reverse('accounts:activate', kwargs={'code': code})),
    }

    send_mail(email, 'activate_profile', context)


def send_activation_change_email(request, email, code):
    context = {
        'subject': _('Change email'),
        'uri': request.build_absolute_uri(reverse('accounts:change_email_activation', kwargs={'code': code})),
    }

    send_mail(email, 'change_email', context)


def send_reset_password_email(request, email, token, uid):
    context = {
        'subject': _('Restore password'),
        'uri': request.build_absolute_uri(
            reverse('accounts:restore_password_confirm', kwargs={'uidb64': uid, 'token': token})),
    }

    send_mail(email, 'restore_password_email', context)


def send_forgotten_username_email(email, username):
    context = {
        'subject': _('Your username'),
        'username': username,
    }

    send_mail(email, 'forgotten_username', context)

def make_message_url(request, message_id):

    uri = request.build_absolute_uri(reverse('accounts:message', kwargs={'message_id': message_id}))
    return uri

def encrypt_message(plaintext_message, message_id):
    
    try:
        encryption = {}

        print(type(plaintext_message))
        
        # Create a symmetric key with Pangea-provided material and default parameters
        create_response = pangea_vault.symmetric_generate(
            purpose=KeyPurpose.ENCRYPTION, algorithm=SymmetricAlgorithm.AES128_CFB, name=f"message-id_{message_id}"
        )
        key_id = create_response.result.id
        encryption['key_id'] = key_id

        # Encrypt a message
        encrypt_response = pangea_vault.encrypt(key_id, str2str_b64(plaintext_message))
        cipher_text = encrypt_response.result.cipher_text
        encryption['cipher_text'] = cipher_text

        return encryption
    
    except pe.PangeaAPIException as e:
        print(f"Vault Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")

def decrypt_message(key_id, cipher_text):

    print("this ran")
    
    try:
        # Decrypt a message
        decrypt_response = pangea_vault.decrypt(key_id, cipher_text)
        plain_text = base64.b64decode(decrypt_response.result.plain_text).decode("ascii")

        return plain_text
    
    except pe.PangeaAPIException as e:
        print(f"Vault Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")