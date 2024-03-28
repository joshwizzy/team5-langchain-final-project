To enable authentication:

- in your `.env` file set `DISABLE_AUTHENTICATION=False`
- copy the sample `config.yaml.example` file to `config.example`
- change the username to your preferred username
- Change the plain text password to a hashed password

You can generate a password hash by running this code

```
import streamlit_authenticator as stauth
stauth.utilities.hasher.Hasher(['abc']).generate()
```
