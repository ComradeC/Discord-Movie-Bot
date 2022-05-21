# Discord-Movie-Bot

Commands:

   * add_movie       
     * Добавляет фильм в список, чтобы посмотреть его позже
     * Лучше в кавычках
   * delete_movie_DB 
     * Удаляет фильм из базы данных
   * movies_db_all  
     * Печатает список всех фильмов в БД
   * movies_to_watch 
     * Печатает список еще несмотренных фильмов в БД
   * add_quote_db
     * Увековечивает цитату в золотом фонде
     * Сначала цитата в кавычках, затем опционально в любом порядке тайминг через двоеточия и фильм-источник в кавычках. Источник должен быть заранее внесен в базу.        
     * Например: 
       * !запиши "У тебя голос Осамы, но у меня сила Обамы" "Полицейский с Рублевки" 00:03:22
   * delete_quoteDB 
     * Удаляет цитату из фонда
   * quotesDB        
     * Ваш карманный фонд золотых цитат
  

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
