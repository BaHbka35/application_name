User API - /users/
## User registration
**POST signup/**
Input:
```
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
```
	{
	"first_name": "some_first_name",
	"surname": "some_surname",
	"username": "some_usename",
	"email": "some_email@email.com"
	}
```
if not:
	status: 400 bad request
	
## User account activation
**GET activate_account/<user_id>/<activation_token>**
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
		```
		{
		"token": "some_token",
		}
		```
	if not:
		status: 400 bad request
		
## User logout
!!! User must be logined
**GET logout/**
Input: {}
Output:
	If success:
		status: 200 ok
	If not:
		status 400 bad request

## Change user password
!!! User must be logined
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
!!! User must be logined
**DELETE delete_user_account/**
Input: {}
Output:
	If success:
		status: 200 ok
	if not:
		status 400 bad request
		
## Update user data
!!! User must be logined
**PUT update_user_data/**
Input:
```
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
!!! User must be logined
**GET users_list/**
Input: {}
Output:
	If success:
		status: 200 ok
		```
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