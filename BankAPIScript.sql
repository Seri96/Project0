create table client (
	client_id serial primary key,
	username varchar(30) not null,
	accounts int4[]
);

create table account(
	account_id serial primary key,
	balance float8,
	client_id int not null ,
	foreign key (client_id) references client(client_id) on delete cascade on update cascade
);



drop table client cascade;
drop table account cascade;


select * from client;
select * from account;
select * from client a inner join account s on a.client_id = s.client_id;
 