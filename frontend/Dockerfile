# Base image olarak nginx kullanıyoruz
FROM nginx:alpine

# Çalışma dizinini /usr/share/nginx/html içine ayarlıyoruz
WORKDIR /usr/share/nginx/html

# Lokaldeki frontend dosyalarını konteynere kopyalıyoruz
COPY . .

# Nginx'i çalıştırıyoruz
CMD ["nginx", "-g", "daemon off;"]
