const Pangea = require("pangea-node-sdk");
const pangeaDomain = process.env.PANGEA_DOMAIN;

const clientIpAddress = (req) => {
    return req?.headers["origin"] || req?.socket.remoteAddress || "localhost";
  };
  
  const hostIpAddress = (req) => {
    return req?.headers["host"] || req?.hostname || "localhost";
  };