
/* Enable pgvector extension */
create extension if not exists vector;

/* Documentation chunks */
/* OpenAI embeddings are 1536 dimensions */
create table site_pages
(
    id bigserial primary key,
    url varchar not null,
    chunk_number integer not null,
    title varchar not null,
    summary varchar not null,
    content text not null,
    metadata jsonb not null default '{}'::jsonb,
    embedding vector(1536),
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,

    unique(url, chunk_number)
);

/* Index for better vector similarity search performance */
create index idx_site_pages_embedding on site_pages using ivfflat (embedding vector_cosine_ops);

/* Index on metadata for faster filtering */
create index idx_site_pages_metadata on site_pages using gin (metadata);

/* Create a function to search for documentation chunks */
create function match_site_pages (
  query_embedding vector(1536),
  match_count int default 10,
  filter jsonb DEFAULT '{}'::jsonb
)
returns table
(
  id bigint,
  url varchar,
  chunk_number integer,
  title varchar,
  summary varchar,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    url,
    chunk_number,
    title,
    summary,
    content,
    metadata,
    1 - (site_pages.embedding <=> query_embedding) as similarity
  from site_pages
  where metadata @> filter
  order by site_pages.embedding <=> query_embedding
  limit match_count;
end;
$$;

/* Supabase row level security */
alter table site_pages enable row level security;

/* Supabase allow public read access */
create policy "Allow public read access"
on site_pages for select to public using (true);


/* Alter the site_pages table to store larger embeddings */
-- Remove index, 4096 dimensions exceeds pgsql 8KB page size limits!
-- https://github.com/pgvector/pgvector/issues/461
drop index site_pages_embedding_idx;

alter table site_pages alter column embedding
set data type vector(3072);

/* Create an equivalent function for the larger embeddings */
create function match_site_pages_3k (
  query_embedding vector(3072),
  match_count int default 10,
  filter jsonb DEFAULT '{}'::jsonb
)
returns table
(
  id bigint,
  url varchar,
  chunk_number integer,
  title varchar,
  summary varchar,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    url,
    chunk_number,
    title,
    summary,
    content,
    metadata,
    1 - (site_pages.embedding <=> query_embedding) as similarity
  from site_pages
  where metadata @> filter
  order by site_pages.embedding <=> query_embedding
  limit match_count;
end;
$$;