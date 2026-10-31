# Local demo administrator setup

Keep the ordinary demo account unchanged so it can still verify standard-user access restrictions. A duplicate registration email cannot be reused for another account, regardless of capitalization. The database traceback from the original createsuperuser command did not create a new administrator.

From smart-expense with its virtual environment active:

```bash
export DB_ENGINE=sqlite
python manage.py create_demo_admin --username se_admin --email se-admin@example.test
```

Enter a strong password twice. No email is sent by this command; the address is synthetic local demonstration data. If these demo identifiers already exist, choose new unique values. The command rejects existing emails with a clear message and does not elevate an existing standard account.

In a separate private browser session open http://127.0.0.1:8000/django-admin/ and sign in as se_admin. Create a disposable test user, deactivate it and inspect Audit events. Never capture passwords in the video or share them in chat. Full manual admin mutation/audit acceptance remains pending until the user supplies the results.
