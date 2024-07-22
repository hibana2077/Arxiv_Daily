FROM node:22.5.1

RUN apt update && apt install -y curl wget iputils-ping

# Create app directory

WORKDIR /app

# Bundle app source
COPY . .

RUN npm install

RUN npm run build

EXPOSE 4321

# HOST=0.0.0.0 PORT=4321 node ./dist/server/entry.mjs

CMD ["node", "./dist/server/entry.mjs"]