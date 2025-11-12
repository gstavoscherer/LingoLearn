FROM node:18 AS build
WORKDIR /app

# Copia package.json e instala dependências
COPY package*.json ./
RUN npm install

# Copia o código e faz o build
COPY . .
RUN npm run build

# Produção - usa apenas as dependências necessárias
FROM node:18-slim
WORKDIR /app

# Copia apenas o build e dependências de produção
COPY --from=build /app/build ./build
COPY --from=build /app/package*.json ./
RUN npm ci --production --ignore-scripts

# Expõe a porta 3000 (padrão do adapter-node)
EXPOSE 3000

# Inicia o servidor
CMD ["node", "build/index.js"]
