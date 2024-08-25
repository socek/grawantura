create policy "Enable read access for all users"
on "public"."answer_logs"
as permissive
for select
to public
using (true);


create policy "Enable read access for all users"
on "public"."answer_player_log"
as permissive
for select
to public
using (true);


create policy "Enable insert for authenticated users only"
on "public"."games"
as permissive
for insert
to authenticated
with check (true);


create policy "Enable read access for all users"
on "public"."instances"
as permissive
for select
to public
using (true);


create policy "Enable read access for all users"
on "public"."players"
as permissive
for select
to public
using (true);



