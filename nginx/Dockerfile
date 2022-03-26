FROM nginx:1.19.10
# 添加blog-nginx博客后台的纯vue
ADD ../vue-element-admin-front/dist /usr/share/nginx/html

VOLUME [ "./nginx.conf:/etc/nginx/conf.d/nginx.conf" ]