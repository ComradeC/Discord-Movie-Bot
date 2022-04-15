# Discord-Movie-Bot

Commands:

 * add_movie, am, д_фильм <фильм>- Добавляет фильм в список
 * movies, movie, кино, фильмы - Создает тред со списком фильмов
 * delete_movie, dm, у_фильм <фильм> - Удаляет фильм из списка

 * add_quote, aq, д_цитату <цитата> - Добавляет цитату в золотой фонд
 * quotes, quote, цитаты - Создает тред со списком цитат
 * delete_quote, dq, у_цитату <цитата> - Удаляет цитату из списка

 * hello - Поздоровайся, будь человеком
  
 * help <команда> - Предоставляет информацию о команде
  

  

Type !help command for more info on a command.

You can also type !help category for more info on a category.

## Connect to server

Discord bot service is deployed on VPS, IP 31.172.64.48

To connect to the server use the next command: ssh root@31.172.64.48

To get a password log in to https://fornex.com/my/vps under devrookiesquad@gmail.com 

## Useful commands on server

Run service:

*$ pm2 start <main_file_name> --name <your_process_name> --interpreter python3*

Show list of running processes:

*$ pm2 list*

Stop process:

*$ pm2 stop <main_file_name>*

Delete process:

*$ pm2 delete <process_id>*

Docs for pm2 https://pm2.keymetrics.io/docs/usage/quick-start/

## To run bot locally

*$ python <main_file_name>*
