---

Going from Vulnerable to Secure with Pangea's Security Platform as a Service

Map of Pangaea 200 million years ago. Image by Fama Clamosa via Wikimedia Commons.
In April 2023, my role was eliminated and I was laid off, which put me on the job hunt for the second time in just 12 months. Part of the Developer Advocate job hunt includes trying out different products as I research companies, and since I enjoy writing tutorials and since I was already doing most of the work, I figured I'd start sharing my code.

---

It's Usually Not Easy (Or Fun) To Do the Right Thing
While it's true that technology has made our lives a lot easier, technology has also made us a lot more vulnerable. Not only is our digital data so much more accessible but with the advent of cloud computing and distributed systems, our data and the infrastructure it lives on have also become increasingly easier to compromise. It seems like not a day goes by without news of a high-profile digital security breach.
As a developer - and therefore one of the people behind the implementation of data-collecting applications running on resources and services scattered throughout the cloud - I know that security is important. And - for better or for worse - I also know that the allure of and the pressure for developing new features at velocity can mean that security takes a backseat, resurfacing with friction down the line when the security team finds a problem and sends me back to the drawing board. In the best-case scenarios, you end up a sprint behind schedule. In the worst-case scenarios, an absently hardcoded secret that was never supposed to go to production ends up in the hands of people you really, really don't want to have to deal with. This can not only cost a company financially in the form of fines and penalties but also put a dent in their reputation.
And the post-mortems are excruciating.
I want to do the right thing. I know I need to eat my vegetables just like I know I need to think about security as much as I think about naming my variables.
Pangea might be one of the closest services I've found to the equivalent of dipping celery sticks in Ranch dressing. Pangea is a Security Platform as a Service. Pangea takes advantage of an API-first framework to deliver cybersecurity services similar to the ways Twilio and Stripe have simplified communications and payments via a developer-first approach to implementation.
In other words, you're already using APIs in your services to do everything else you don't want to have to think about, so why not use the same idea to implement best security practices? Moreover, by offloading the responsibility to a company with a legacy of experience in the field, you get to focus more on innovation and less on having to reinvent and maintain the wheel.
This post will take you on a tour of a small Python Django sample application that will allow you to experience first-hand just how accessible and valuable Pangea can be. While this sample probably isn't something you'd push to production, its intention is to demonstrate the feasibility of Pangea and hint at its possibilities.
In case you have a brain like mine that seems to have a severe distaste for following tutorials in a linear manner (thanks ADHD!), I have outlined the post and listed the tutorial components and resources and references below so you can choose your own adventure:
Outline
Prerequisites
Pangea Account and Project Setup
The Sample Code Explained
Pangea Vault Implementation
Pangea Secure Audit Log Implementation
Pangea Redact Implementation
In Conclusion
Resources and References

Tutorial Components
Pangea account
Sample app code on GitHub

Prerequisites
Python 3.7+
A Pangea account
Enough familiarity with Python, APIs, and the Django web app framework to muddle through some basic concepts and functions

Pangea Account and Project Setup
Pangea Cyber
Taking its name from the prehistoric supercontinent that once connected all the land masses of planet Earth, Pangea offers everything you need to establish a strong security posture without having to devote resources to building the tools and services yourself. In this particular sample, you will be using the following Pangea services: Secure Audit Log, Redact, and Vault. You will use these services to create a sample application that enables encrypted messaging between patients and providers with a tamper-proof log of user activity that also redacts sensitive information.
Creating a Pangea Account and Configuring Different Services
Creating a Pangea account is as easy as signing into GitHub. Once you authorize access, you'll be able to log into your Pangea Console and read the Pangea docs. Follow the Getting Started guide to create your first organization and project. For this particular sample app, you won't need to invite any additional users.
Pangea offers a range of security services, but as mentioned above, for this sample, you will use Secure Audit Log, Redact, and Vault. Follow the documentation here to configure these services. When you create your token, you can select additional services to allow the token access to all at the same time so you don't have to repeat the process for each one.
You can select multiple services at once for a single token.Now that you've got things set up on the Pangea side, it's time to take a look at the code.
The Sample Code Explained
A Quick Tour of the Sample Code
The code is available here and you can pull it down with the following:
git clone https://github.com/liz-acosta/lab-pangea.git
The code you want is in the folder labeled pangea-django-exampleand it is derived from the Pangea sample code from their repository on GitHub. You can use the Pangea tutorial for Integrating with Django as a complement to this post.
The sample I've provided follows a typical Django project structure and uses Pipenv to manage the project's dependencies and virtual environment. This sample is mostly concerned with the contents of the acountsand appsubdirectories within the sourcedirectory of pangea-django-example.
Running the Code Locally
1. Before running anything make sure you are located in the pangea-django-example directory. (I mention this because I've screwed up this basic, critical step more times than I'd like to admit!)
2. Update `Pipfile` with the following Pangea dependencies:
pangea-sdk = "*"
django-environ = "*"
3. Install the project dependencies by first installing Pipenv and then installing the dependencies with the following commands:
pip install pipenv
pipenv install
4. Activate your virtual environment via the command pipenv shell. You should notice that your prompt is prefixed with the name of the virtual environment in parentheses.
5. Add your Pangea variables by updating the .env.example file located in source/app/conf/development and renaming it from .env.example to .env. Populate the new .env file with the following:
PANGEA_DOMAIN='REPLACE-WITH-YOUR-PANGEA-DOMAIN'
PANGEA_TOKEN='REPLACE-WITH-YOUR-PANGEA-TOKEN'
Your Pangea domain can be found in the Pangea Console UI on the right-hand side of the "Home" > "Dashboard" page.
Use the copy icon to copy your Domain and add it to the .env file.Your Pangea token can be found in the Pangea Console UI under "Project Settings" > "Tokens" in the menu on the left-hand side of the page.
Locate and copy your token in the Pangea Console UI and add it to your .env file.Note! If you are planning on pushing this code anywhere public, make sure to add source/app/conf/development/.env to the .gitignore file so you don't accidentally expose your Pangea tokens! (If you're trying to find the .gitignore file associated with this project in the repo, it's located in the pangea-django-example/ directory here. Yes, the file structure in the repo is unconventional.)
(I've accidentally pushed secrets SO MANY TIMES and as a result, have unnecessarily extensive knowledge of rewriting history in Git. And yes, you can use Pangea to store your Pangea secrets - maybe that will be my next tutorial!)
6. Set up the database. django-admin is Django's command-line utility and its available tasks can be found in source/manage.py.
This sample app makes use of Django's User model in its startproject default project template and creates two additional models: Activation and Message. Message is the model this sample app is most concerned with and you can find the models.py file in the source/accounts/directory.
Use the following commands to set up your database:
python3 source/manage.py makemigrations
python3 source/manage.py migrate
7. Now run the app with the following:
python3 source/manage.py runserver
8. In your browser, navigate to localhost:8000, and there, you should be greeted with an account creation page. Create a test patient account using a first and last name that could be a real name and don't use something like "Test One". You'll see why later. (Hint: It has to do with the Redact part of this tutorial.) You can, however, provide a nonfunctional email address.
A Quick Tour of the App
In this very rudimentary and not-too-aesthetically pleasing app, you will notice a few options in the navbar at the top of the page. For this sample, you will be mostly using the "Messages", "Send message", and "Log out" options. "Messages" is where a user can see a list of messages sent to them and "Send message" is where a user can write and send a message.
However, in order to use these functions, you need at least two users. Log out of the app, create a test provider user similar to your test patient user, and log back in as the test provider. Try sending a message to the test provider user, then log back out and log back in as the test provider user. If everything is working correctly, you should see a list of messages on the "Messages" page and you should be able to click on the message subject to read the message body.
If your app is set up and working correctly, you should see something like this.A Look at the Database
1. Open up a new terminal tab and follow the steps in the "Running the Code Locally" section above to set up and activate your virtual environment. In this tab, you are going to access the app's database.
2. Use the following command to activate a database shell:
python3 source/manage.py dbshell
The shell prompt will look like this: sqlite>
3. Configure the shell so your tables are in a more human-readable tabular form by using the following commands:
.header on
.mode markdown
4. Now query the messages table with the following:
select * from accounts_message;
You should get something like this:
id  message                         key_id            timestamp                   recipient_id  sender_id  subject                   read_status
--  ------------------------------  ----------------  --------------------------  ------------  ---------  ------------------------  -----------
1   This is a test message                            2023-06-10 01:40:12.178828  1             2          This is a test subject    0      
Notice something about the message? The body is in plaintext which is potentially in violation of certain data privacy and security regulations. Fortunately, Pangea makes it easy to generate cryptographic keys and encrypt and decrypt messages - and guess what? They will even manage the keys for you.
A Quick Note about Using The Code
In an effort to make using this sample easier for you, all the code you need is already present and commented out so you can uncomment the code as you follow along with the tutorial. I have tried to indicate which lines of code to manipulate by using TODO in the comments. This way you can do a search for TODO and hopefully easily find the code you need to change.
Pangea Vault
Pangea Vault provides secure storage of secrets, cryptographic keys, and Pangea API Tokens tokens as Vault items. With Vault, you can easily generate, import, and manage secrets and keys to remain compliant and secure by never exposing keys in your applications. One less thing to worry about!
To learn more about Pangea Vault, read the overview here.
In order to use Vault in this sample app, perform the following:
1. Open up the file named views.py in source/accounts/ and find the following code within the MessageSendView class:
#TODO: Uncomment the code below:
## Encrypt the message body using Pangea Vault
# encryption = encrypt_message(form.cleaned_data['message'], message.id)

## Log the encryption event
# pangea_audit.log(f"Encrypting message from {user} to {message.recipient}")

# m = Message.objects.get(id=message.id)
# m.message = encryption['cipher_text']
# m.key_id = encryption['key_id']
# m.save()
As the TODO comment indicates, uncomment the code.
Now comment out the following code:
# TODO: Comment the one line of code below:
message.message = form.cleaned_data['message']
2. Now return to your locally running app UI and send another message.
3. Check the database and use the select * from accounts_message; query again - notice anything about the new message? It should be encrypted. Now try to read the new message in the app. The message should still be encrypted. You now need to add a way to decrypt it.
4. Return to the views.py file and find the MessageView class. Similar to Step 1 above, find the following code and uncomment it:
## Decrypt the ciphertext
# plain_text = decrypt_message(message.key_id, message.message)
# message_object['message'] = plain_text
And comment out the following code:
message_object['message'] = message.message
5. Refresh the message in the app UI. Is it in plaintext now?
So What's Happening Here?
In both of the scenarios above, the code is referencing a function in the utils.py file located in source/accounts/.
Take a look at utils.py and find the encrypt_message and decrypt_message functions. Both of these functions use Pangea Vault to perform all the necessary cryptographic operations. encrypte_message contains the additional step of generating the symmetric key that is used in both the encryption and decryption of the message. When the key is generated, it is assigned a Pangea id. This id is saved with the message in the database so it can be used to decrypt the ciphertext stored there.
An instance of Pangea Vault is initialized at the top of the file using the Pangea configuration and the Pangea token you added to the .env file. This is the instance used to generate the cryptographic keys and perform encryption and decryption.
pangea_config = PangeaConfig(domain=settings.PANGEA_DOMAIN)
pangea_vault = Vault(settings.PANGEA_TOKEN, config=pangea_config)
You can see your keys and their ids in the Pangea Console UI under "Vault" > "Secrets & Keys" in the menu on the left-hand side of the page.
Find your Secrets & Keys in the Pangea Console UI.Pangea Secure Audit Log
Pangea Secure Audit Log is a record of events or actions stored in a tamper-proof manner to ensure the integrity and accuracy of the information.
A secure audit log can be used to detect security breaches, unauthorized access, or other malicious activities within a system. By providing a complete and accurate record of all system events, a secure audit log can help organizations maintain compliance with legal and regulatory requirements, as well as improve their overall security posture.
To learn more about Pangea Secure Audit Log, read the overview here.
When you uncommented the encryption code above, you might have noticed that you also uncommented the audit logging code.
In order to see the logs, navigate to your Pangea Console and then to "Secure Audit Logs" > "View Logs" in the menu on the left-hand side of the page.
View your logs in the Pangea Console UI.What's Happening Here?
In the views.py file, look for the following code in the LogInView class:
pangea_audit.log("User: " + request.user.username+ " logged into the app")
This code uses the instance of Pangea Audit initialized at the top of the file to call the Audit endpoint and record a log. Where else might you want to add logging to this app?
pangea_config = PangeaConfig(domain=settings.PANGEA_DOMAIN)
pangea_audit = Audit(settings.PANGEA_TOKEN, config=pangea_config)
Now check the logs in the Pangea Console. Do you notice a log indicating when a message was opened?
This specific log displays a first and last name in plaintext.This particular log records a first and last name which can be classified as PII and therefore in violation of certain privacy and security regulations. This is data you might want to redact.
Pangea Redact
Pangea Redact helps developers limit the sprawl of sensitive information by omitting or masking data using defined rules. Redact comes equipped with out-of-the-box redaction rules to identify personally identifiable information (PII), payment card industry (PCI) data, and other sensitive information.
To learn more about Pangea Redact, read the overview here.
In order to use Redact in this sample app, perform the following:
1. In the views.py file, find the MessageView class and look for the following code:
# pangea_audit.log(f"{user} opened message from {pangea_redact.redact(message_object['sender']).result.redacted_text}")
Uncomment this code and comment out the following code:
pangea_audit.log(f"{user} opened message from {message_object['sender']}")
2. In your Pangea Console, navigate to "Redact" > "Rulesets". In the "PII" ruleset, enable the "Person" rule and select "Partial Mask" from the "Redaction Method" dropdown.
Create your Rulesets from the Redact menu in the Pangea Console UI.Create your Ruleset in the Pangea Console UI.3. Now refresh the message in the app and check the logs. What's different about them now?
What's Happening Here?
Similar to Vault and Secure Audit Log above, Pangea Redact is initialized at the top of the file. This instance is then used to redact the full name from the audit log in the following code:
pangea_audit.log(f"{user} opened message from {pangea_redact.redact(message_object['sender']).result.redacted_text}")
Remember how I mentioned using a real name to create your user accounts? This is why. The Pangea PII Person ruleset pattern matching won't recognize something like "Test One" as a name and therefore, will not redact it. You can set custom rulesets with Pangea that go beyond the capabilities of what Pangea provides out of the box.
In Conclusion
In just a few short steps, you've made this sample app a lot more secure without having to set up any additional infrastructure or services you or your organization have to maintain. Built with engineers in mind, Pangea is security that works with developers and existing project conventions to preserve production velocity and go to market faster.
To learn more about Pangea, check out the blog or pull down the code from GitHub.
Resources and References
Introducing Security Platform as a Service
Pangea Documentation
Meet Django: The web framework for perfectionists with deadlines
Pipenv: Python Dev Workflow for Humans
(And in case you run into the same errors I ran into while trying to install Pipenv: brew install pipenv)
Rewriting your git history, removing files permanently [cheat sheet included]
What is PII?
