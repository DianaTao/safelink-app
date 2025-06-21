import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://ccotkrhrqkldgfdjnlea.supabase.co'
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
const supabaseServiceKey = process.env.SUPABASE_KEY

// Client-side Supabase client (for browser)
export const supabase = createClient(supabaseUrl, supabaseAnonKey!)

// Server-side Supabase client (for API routes)
export const supabaseAdmin = createClient(supabaseUrl, supabaseServiceKey!)

// Helper functions for common operations
export const auth = {
  signUp: (email: string, password: string) => 
    supabase.auth.signUp({ email, password }),
  
  signIn: (email: string, password: string) => 
    supabase.auth.signInWithPassword({ email, password }),
  
  signOut: () => supabase.auth.signOut(),
  
  getUser: () => supabase.auth.getUser(),
  
  onAuthStateChange: (callback: any) => 
    supabase.auth.onAuthStateChange(callback)
}

export const database = {
  // Example: Get saved rentals for a user
  getSavedRentals: (userId: string) =>
    supabase.from('saved_rentals').select('*').eq('user_id', userId),
  
  // Example: Save a rental listing
  saveRental: (rentalData: any) =>
    supabase.from('saved_rentals').insert(rentalData),
  
  // Example: Get user profile
  getUserProfile: (userId: string) =>
    supabase.from('profiles').select('*').eq('id', userId).single()
} 