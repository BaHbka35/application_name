Challenge API - /challenges/
## Create challenge
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
if success:
	status: 200 ok
if not: 
	status: 400 bad request