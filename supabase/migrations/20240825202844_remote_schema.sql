create table "public"."answer_logs" (
    "id" uuid not null default gen_random_uuid(),
    "created_at" timestamp with time zone not null default now(),
    "instance_id" uuid,
    "question_id" uuid
);


alter table "public"."answer_logs" enable row level security;

create table "public"."answer_player_log" (
    "id" uuid not null default gen_random_uuid(),
    "created_at" timestamp with time zone not null default now(),
    "answer_log_id" uuid,
    "player_id" uuid,
    "points_auctioned" bigint default '0'::bigint
);


alter table "public"."answer_player_log" enable row level security;

create table "public"."instances" (
    "id" uuid not null default gen_random_uuid(),
    "created_at" timestamp with time zone not null default now(),
    "game_id" uuid
);


alter table "public"."instances" enable row level security;

create table "public"."players" (
    "id" uuid not null default gen_random_uuid(),
    "created_at" timestamp with time zone not null default now(),
    "name" character varying,
    "instance_id" uuid default gen_random_uuid()
);


alter table "public"."players" enable row level security;

CREATE UNIQUE INDEX answer_log_pkey ON public.answer_logs USING btree (id);

CREATE UNIQUE INDEX answer_player_log_pkey ON public.answer_player_log USING btree (id);

CREATE UNIQUE INDEX instances_id_key ON public.instances USING btree (id);

CREATE UNIQUE INDEX instances_pkey ON public.instances USING btree (id);

CREATE UNIQUE INDEX players_pkey ON public.players USING btree (id);

alter table "public"."answer_logs" add constraint "answer_log_pkey" PRIMARY KEY using index "answer_log_pkey";

alter table "public"."answer_player_log" add constraint "answer_player_log_pkey" PRIMARY KEY using index "answer_player_log_pkey";

alter table "public"."instances" add constraint "instances_pkey" PRIMARY KEY using index "instances_pkey";

alter table "public"."players" add constraint "players_pkey" PRIMARY KEY using index "players_pkey";

alter table "public"."answer_logs" add constraint "answer_log_instance_id_fkey" FOREIGN KEY (instance_id) REFERENCES instances(id) not valid;

alter table "public"."answer_logs" validate constraint "answer_log_instance_id_fkey";

alter table "public"."answer_logs" add constraint "answer_log_question_id_fkey" FOREIGN KEY (question_id) REFERENCES questions(id) not valid;

alter table "public"."answer_logs" validate constraint "answer_log_question_id_fkey";

alter table "public"."answer_player_log" add constraint "answer_player_log_answer_log_id_fkey" FOREIGN KEY (answer_log_id) REFERENCES answer_logs(id) not valid;

alter table "public"."answer_player_log" validate constraint "answer_player_log_answer_log_id_fkey";

alter table "public"."answer_player_log" add constraint "answer_player_log_player_id_fkey" FOREIGN KEY (player_id) REFERENCES players(id) not valid;

alter table "public"."answer_player_log" validate constraint "answer_player_log_player_id_fkey";

alter table "public"."instances" add constraint "instances_game_id_fkey" FOREIGN KEY (game_id) REFERENCES games(id) not valid;

alter table "public"."instances" validate constraint "instances_game_id_fkey";

alter table "public"."instances" add constraint "instances_id_key" UNIQUE using index "instances_id_key";

alter table "public"."players" add constraint "players_instance_id_fkey" FOREIGN KEY (instance_id) REFERENCES instances(id) not valid;

alter table "public"."players" validate constraint "players_instance_id_fkey";

grant delete on table "public"."answer_logs" to "anon";

grant insert on table "public"."answer_logs" to "anon";

grant references on table "public"."answer_logs" to "anon";

grant select on table "public"."answer_logs" to "anon";

grant trigger on table "public"."answer_logs" to "anon";

grant truncate on table "public"."answer_logs" to "anon";

grant update on table "public"."answer_logs" to "anon";

grant delete on table "public"."answer_logs" to "authenticated";

grant insert on table "public"."answer_logs" to "authenticated";

grant references on table "public"."answer_logs" to "authenticated";

grant select on table "public"."answer_logs" to "authenticated";

grant trigger on table "public"."answer_logs" to "authenticated";

grant truncate on table "public"."answer_logs" to "authenticated";

grant update on table "public"."answer_logs" to "authenticated";

grant delete on table "public"."answer_logs" to "service_role";

grant insert on table "public"."answer_logs" to "service_role";

grant references on table "public"."answer_logs" to "service_role";

grant select on table "public"."answer_logs" to "service_role";

grant trigger on table "public"."answer_logs" to "service_role";

grant truncate on table "public"."answer_logs" to "service_role";

grant update on table "public"."answer_logs" to "service_role";

grant delete on table "public"."answer_player_log" to "anon";

grant insert on table "public"."answer_player_log" to "anon";

grant references on table "public"."answer_player_log" to "anon";

grant select on table "public"."answer_player_log" to "anon";

grant trigger on table "public"."answer_player_log" to "anon";

grant truncate on table "public"."answer_player_log" to "anon";

grant update on table "public"."answer_player_log" to "anon";

grant delete on table "public"."answer_player_log" to "authenticated";

grant insert on table "public"."answer_player_log" to "authenticated";

grant references on table "public"."answer_player_log" to "authenticated";

grant select on table "public"."answer_player_log" to "authenticated";

grant trigger on table "public"."answer_player_log" to "authenticated";

grant truncate on table "public"."answer_player_log" to "authenticated";

grant update on table "public"."answer_player_log" to "authenticated";

grant delete on table "public"."answer_player_log" to "service_role";

grant insert on table "public"."answer_player_log" to "service_role";

grant references on table "public"."answer_player_log" to "service_role";

grant select on table "public"."answer_player_log" to "service_role";

grant trigger on table "public"."answer_player_log" to "service_role";

grant truncate on table "public"."answer_player_log" to "service_role";

grant update on table "public"."answer_player_log" to "service_role";

grant delete on table "public"."instances" to "anon";

grant insert on table "public"."instances" to "anon";

grant references on table "public"."instances" to "anon";

grant select on table "public"."instances" to "anon";

grant trigger on table "public"."instances" to "anon";

grant truncate on table "public"."instances" to "anon";

grant update on table "public"."instances" to "anon";

grant delete on table "public"."instances" to "authenticated";

grant insert on table "public"."instances" to "authenticated";

grant references on table "public"."instances" to "authenticated";

grant select on table "public"."instances" to "authenticated";

grant trigger on table "public"."instances" to "authenticated";

grant truncate on table "public"."instances" to "authenticated";

grant update on table "public"."instances" to "authenticated";

grant delete on table "public"."instances" to "service_role";

grant insert on table "public"."instances" to "service_role";

grant references on table "public"."instances" to "service_role";

grant select on table "public"."instances" to "service_role";

grant trigger on table "public"."instances" to "service_role";

grant truncate on table "public"."instances" to "service_role";

grant update on table "public"."instances" to "service_role";

grant delete on table "public"."players" to "anon";

grant insert on table "public"."players" to "anon";

grant references on table "public"."players" to "anon";

grant select on table "public"."players" to "anon";

grant trigger on table "public"."players" to "anon";

grant truncate on table "public"."players" to "anon";

grant update on table "public"."players" to "anon";

grant delete on table "public"."players" to "authenticated";

grant insert on table "public"."players" to "authenticated";

grant references on table "public"."players" to "authenticated";

grant select on table "public"."players" to "authenticated";

grant trigger on table "public"."players" to "authenticated";

grant truncate on table "public"."players" to "authenticated";

grant update on table "public"."players" to "authenticated";

grant delete on table "public"."players" to "service_role";

grant insert on table "public"."players" to "service_role";

grant references on table "public"."players" to "service_role";

grant select on table "public"."players" to "service_role";

grant trigger on table "public"."players" to "service_role";

grant truncate on table "public"."players" to "service_role";

grant update on table "public"."players" to "service_role";


