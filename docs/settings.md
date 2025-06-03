# Settings

| Setting Key | Type      |      Default                              | Required                             |Example|
|-------------|-----------|-------------------------------------------| ------------------------------------ |-------|
|EASY_EMAIL_ATTACHMENT_UPLOAD_PATH| string    | `'easy_email/attachments'`  | No                                   |`'some/other/path'`|
|EASY_EMAIL_ATTACHMENT_STORAGE_BACKEND| string    | `None`, fallback to `DEFAULT_FILE_STORAGE` settings  | No                                   | String dot notation storage path. Ex: `'storages.backends.s3.S3Storage'`|
