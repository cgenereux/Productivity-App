-- Supabase schema for FocusFlow

create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  display_name text,
  created_at timestamptz not null default now()
);

-- Repeating/scheduled tasks the user defines
create table if not exists tasks (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  title text not null,
  type text not null check (type in ('daily','weekly','one_off')),
  duration_min integer,
  percent_tracking boolean not null default false,
  progression_days integer,
  progression_on_miss text check (progression_on_miss in ('hold','reset')),
  weekdays int[] null,
  active boolean not null default true,
  created_at timestamptz not null default now()
);

-- Backlog items awaiting scheduling
create table if not exists backlog (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  title text not null,
  estimate_min integer,
  created_at timestamptz not null default now()
);

-- Materialized instances for a given date (schedule + backlog + quick)
create table if not exists instances (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  task_id uuid references tasks(id) on delete set null,
  date date not null,
  title text not null,
  duration_est integer,
  percent integer,
  completed boolean not null default false,
  actual_min integer not null default 0,
  ord integer not null default 0,
  source text not null check (source in ('schedule','backlog','quick')),
  backlog_id uuid references backlog(id) on delete set null,
  created_at timestamptz not null default now()
);

create index if not exists instances_user_date_idx on instances(user_id, date);

-- Per-user settings
create table if not exists settings (
  user_id uuid primary key references users(id) on delete cascade,
  rollover_hour integer not null default 3,
  progression_miss text not null default 'hold' check (progression_miss in ('hold','reset')),
  updated_at timestamptz not null default now()
);

-- Simple progression state per task
create table if not exists task_progression (
  user_id uuid not null references users(id) on delete cascade,
  task_id uuid not null references tasks(id) on delete cascade,
  day integer not null default 1,
  primary key (user_id, task_id)
);

-- RLS templates (enable and scope rows by auth.uid())
-- alter table users enable row level security;
-- alter table tasks enable row level security;
-- alter table backlog enable row level security;
-- alter table instances enable row level security;
-- alter table settings enable row level security;
-- alter table task_progression enable row level security;

-- create policy "Users can see self" on users for select using (id = auth.uid());
-- create policy "Users manage own tasks" on tasks for all using (user_id = auth.uid()) with check (user_id = auth.uid());
-- ... replicate for backlog, instances, settings, task_progression

