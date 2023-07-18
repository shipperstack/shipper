# FAQ

## I get a "CSRF verification failed" when trying to log in on my development setup. What gives?

This is because you are not connecting to your local server with HTTPS. For
instructions on how to do that, [check out this guide on web.dev](https://web.dev/how-to-use-local-https/).
On macOS, here are the commands you need to run:

```
brew install mkcert
brew install nss
mkcert -install
cd docker/nginx/certs
mkcert localhost
```

And to undo all that:

```
mkcert -uninstall
rm -r $(mkcert -CAROOT)
```