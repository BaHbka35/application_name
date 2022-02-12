Challenge API - /challenges/
## Create challenge
!!! User must be authenticated

If user create a challenge  he automatically stays a challenge member(he accepts challenge)

**POST create_challenge**

input:
```json
{
"name": "challenge_name",
"finish_datetime": "2023-01-30 18:25:43",
"goal": "make 20 pushups in 10 seconds",
"description": "you mush make 20 pushups in 10 seconds and smth else",
"requirements": "stopwatch must be seen on video",
"bet": 50
}
```
"bet" can be 0 or bigger

output:

if success:</br>
>status: 200 ok
> 
if not: 
>status: 400 bad request


## Upload video example for challenge
!!! User must be authenticated

**PUT upload_video_example/<challenge_id>/**

type = multipart/form-data

you can upload only mp4 format

input:
```multipart/form-data
{'video_example': video_file.mp4}
```

output:

if success:
> status: 200 ok

if not:
> status: 400 bad request


## Accept challenge
!!! User must be authenticated

**GET accept_challenge/challenge_id/**

input: {}

output:

if success:
> status: 200 ok

if not:
> status: 400 bad request


## Get challenges list
**GET get_challenges_list/**

you will receive only challenges that are active

input: {}

if success:
> status: 200 ok
```json
[
  {
    "name": "challenge_name2",
    "goal": "make 20 pushups in 10 seconds",
    "bet": 0,
    "finish_datetime": "2023-02-02 18:25:43",
    "challenge_id": 5,
    "creator": "Luk",
    "members_amount": 2,
    "bets_sum": 0
  },
  {
    "name": "challenge_name",
    "goal": "make 20 pushups in 10 seconds",
    "bet": 50,
    "finish_datetime": "2023-02-02 18:25:43",
    "challenge_id": 6,
    "creator": "Luk",
    "members_amount": 2,
    "bets_sum": 100
  }
]
```

if not:
> status: 400 bad request


## Get detail information about challenge.
!!! User must be authenticated.

**GET get_detail_challenge/challenge_id/**

input: {}

output:

if success:
> status: 200 ok
```json
{
  "name": "challenge_name2",
  "goal": "make 20 pushups in 10 seconds",
  "bet": 0,
  "finish_datetime": "2023-02-02 18:25:43",
  "description": "you mush make 20 pushups in 10 seconds",
  "requirements": "stopwatch must be seen on video",
  "challenge_id": 5,
  "creator": "Luk",
  "members_amount": 2,
  "bets_sum": 0,
  "video_example_path": "/home/user/application_name/backend/media/video_examples/3_5.mp4"
}
```

If challenge hasn't video example field "video_example_path" will be None

if not:
> status: 400 bad request



## Get challenge member
!!! User must be authenticated.

**GET get_challenge_members/challenge_id/**

input: {}

output:

if success:
> status: 200 ok
```json
[
  {
    "user_id": 1,
    "username": "Luk"
  },
  {
    "user_id": 3,
    "username": "Luk2"
  }
]
```

if not:
> status: 400 bad request
