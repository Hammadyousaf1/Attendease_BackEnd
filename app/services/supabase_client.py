from supabase import create_client

SUPABASE_URL = "https://arlexrfzqvahegtolcjp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFybGV4cmZ6cXZhaGVndG9sY2pwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg2ODE4MjcsImV4cCI6MjA1NDI1NzgyN30.ksThqyqHmQt16ZmlYM7hrutQVmBOcYt-0xap6a7QlhQ"

supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client():
    return supabase_client