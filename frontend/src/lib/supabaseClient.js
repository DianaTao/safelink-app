import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://ccotkrhrqkldgfdjnlea.supabase.co'
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
const supabaseServiceKey = process.env.SUPABASE_KEY

// Only create Supabase client if we're in the browser and have the key
const createSupabaseClient = () => {
  if (typeof window === 'undefined') {
    // Server-side: return a mock client
    return {
      auth: {
        signUp: () => Promise.resolve({ error: null }),
        signInWithPassword: () => Promise.resolve({ error: null }),
        signOut: () => Promise.resolve({ error: null }),
        getUser: () => Promise.resolve({ user: null, error: null }),
        onAuthStateChange: () => ({ data: { subscription: { unsubscribe: () => {} } } })
      },
      from: () => ({
        select: () => ({
          eq: () => ({
            single: () => Promise.resolve({ data: null, error: null }),
            limit: () => Promise.resolve({ data: null, error: null })
          }),
          single: () => Promise.resolve({ data: null, error: null }),
          limit: () => Promise.resolve({ data: null, error: null })
        }),
        insert: () => Promise.resolve({ data: null, error: null })
      })
    }
  }

  if (!supabaseAnonKey) {
    console.warn('NEXT_PUBLIC_SUPABASE_ANON_KEY is not set')
    return null
  }

  return createClient(supabaseUrl, supabaseAnonKey)
}

// Client-side Supabase client (for browser)
export const supabase = createSupabaseClient()

// Server-side Supabase client (for API routes)
export const supabaseAdmin = typeof window === 'undefined' && supabaseServiceKey 
  ? createClient(supabaseUrl, supabaseServiceKey)
  : null

// Helper functions for common operations
export const auth = {
  signUp: (email, password) => 
    supabase?.auth.signUp({ email, password }) || Promise.resolve({ error: { message: 'Supabase not initialized' } }),
  
  signIn: (email, password) => 
    supabase?.auth.signInWithPassword({ email, password }) || Promise.resolve({ error: { message: 'Supabase not initialized' } }),
  
  signOut: () => 
    supabase?.auth.signOut() || Promise.resolve({ error: { message: 'Supabase not initialized' } }),
  
  getUser: () => 
    supabase?.auth.getUser() || Promise.resolve({ user: null, error: { message: 'Supabase not initialized' } }),
  
  onAuthStateChange: (callback) => 
    supabase?.auth.onAuthStateChange(callback) || { data: { subscription: { unsubscribe: () => {} } } }
}

export const database = {
  // Example: Get saved rentals for a user
  getSavedRentals: (userId) =>
    supabase?.from('saved_rentals').select('*').eq('user_id', userId) || Promise.resolve({ data: null, error: { message: 'Supabase not initialized' } }),
  
  // Example: Save a rental listing
  saveRental: (rentalData) =>
    supabase?.from('saved_rentals').insert(rentalData) || Promise.resolve({ data: null, error: { message: 'Supabase not initialized' } })
}

// Separate function for getting user profile to avoid TypeScript issues
export const getUserProfile = (userId) => {
  if (!supabase) {
    return Promise.resolve({ data: null, error: { message: 'Supabase not initialized' } })
  }
  try {
    return supabase.from('profiles').select('*').eq('id', userId).single()
  } catch (error) {
    return Promise.resolve({ data: null, error: { message: 'Supabase query failed' } })
  }
} 