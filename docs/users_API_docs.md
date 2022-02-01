User API - /users/
## User registration
**POST signup/**

Input:
```json
	{
	"first_name": "some_first_name",
	"surname": "some_surname",
	"username": "some_usename",
	"email": "some_email@email.com",
	"password": "some_password",
	"password2": "some_password"
	}
```
Output:

if registration was successful:
	status: 201 ok

```json
	{
	"first_name": "some_first_name",
	"surname": "some_surname",
	"username": "some_usename",
	"email": "some_email@email.com",
	"message": "Check your email for activate account"
	}
```
if not:
	status: 400 bad request

After that user must get email letter with activation link.

## User account activation
**GET activate_account/<user_id>/<encrypted_datetime>/<activation_token>**

This link must be received on the email of the user. 

Lifetime of activation link is 24 hours

Input: {}
Output:
	if success:
		status: 200 Ok
	if not:
		status: 400 bad request
		

## User login
**POST login/**

Input:
```
	{
	"username": "some_usename",
	"password": "some_password",
	}
```
Output:
	if success:
		status: 200 Ok
```json
	{
		"token": "some_token",
		"signature": "some_signature",
	}
```

if not:
		status: 400 bad request

### Important.
When User must be authenticated, server must get request with headers:
- Token
- Signature

## User logout
!!! User must be authenticated
**GET logout/**

Input: {}
Output:
	If success:
		status: 200 ok
	If not:
		status 400 bad request

## Change user password
!!! User must be authenticated
**PUT change_user_password/**

Input: 
```
	{
	"old_password": "some_old_password",
	"new_password": "new_password",
	"new_password2": "new_password",
	}
```
Output:
	If success:
		status: 200 ok
	if not:
		status 400 bad request

## Delete user account
!!! User must be authenticated
**DELETE delete_user_account/**

Input: {}
Output:
	If success:
		status: 200 ok
	if not:
		status 400 bad request
		
## Update user data
!!! User must be authenticated
**PUT update_user_data/**

Input:
```json
{
    'first_name': 'some_first_name',
    'surname': 'some_surname',
    'username': 'some_username',
    'age': 18,
    'gender': 'male or female',
    'training_experience': 4.5,
    'trains_now': True or False,
}
```
Output:
	If success:
		status: 200 ok
	if not:
		status 400 bad request

## Get users list
!!! User must be authenticated
**GET users_list/**

Input: {}
Output:
	If success:
		status: 200 ok
```json
	[
		{"first_name": "some_first_name1",
		"surname": "some_surname1",
		"username": "some_username1"},
		{"first_name": "some_first_name2",
		"surname": "some_surname2",
		"username": "some_username2"},
	]	
```

if not:
	status 400 bad request
	
## Change user email
!!! User must be authenticated
**GET change_user_email/**

Input: 
```json
{
	"new_user_email": "some@email.xxx"
}
```
Output:
	If success:
		status: 200 ok
	If not:
		status: 400 bad request
User must get email on new email with confirmation link

## Confirm user email
**GET email_confirmation/user_id/encrypted_datetime/token/**

This link must be received on the new email of the user.

Lifetime of activation link is 24 hours

Input: {}
Output:
	if success:
		status: 200 ok
	if not:
		status: 400 bad request