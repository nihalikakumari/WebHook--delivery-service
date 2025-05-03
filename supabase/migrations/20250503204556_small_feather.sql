/*
  # Add event_types to subscriptions table

  1. Changes
    - Add event_types ARRAY column to subscriptions table
    
  2. Notes
    - Uses ARRAY type to store multiple event types
    - Allows NULL for optional event type filtering
*/

DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'subscription' AND column_name = 'event_types'
  ) THEN
    ALTER TABLE subscription ADD COLUMN event_types text[] NULL;
  END IF;
END $$;