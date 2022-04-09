# Discord-Movie-Bot

No Category:

 * add_movie Добавляет фильм в список
  
 *  add_quote Добавляет цитату в золотой фонд
  
 *  hello     Поздоровайся, будь человеком
  
 *  help      Shows this message
  
 *  movies    Печатает список фильмов
  
 *  quotes    Ваш карманный фонд золотых цитат
  

Type !help command for more info on a command.

You can also type !help category for more info on a category.

## Connect to server

Discord bot service is deployed on VPS, IP 31.172.64.48

To connect to the server use the next command: ssh root@31.172.64.48

To get a password log in to https://fornex.com/my/vps under devrookiesquad@gmail.com 

## Useful commands on server

Run service:

*$ pm2 start <main_file_name> --name <your_bot_name> --interpreter python3*

Show list of running processes:

*$ pm2 list*

Stop process:

*$ pm2 stop <main_file_name>*

Delete process:

*$ pm2 delete <process_id>*

## To run bot locally

*$ python bot.py*
