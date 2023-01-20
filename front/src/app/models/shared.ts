export interface Token {
  access_token: string;
  token_type: string;
  expiration: number;
}

export interface User {
  username: string;
}

export interface SlotObj {
  date: string;
  id: number;
  status: number;
}

export interface GetWeekResponse {
  [key: string]: { [key: number]: number };
}

export interface WeekDatesSlots {
  [key: string]: { [key: number]: SlotObj };
}

export interface BookSlotResponse {
  username: string;
  full_name: string;
  date: string;
  slot_id: number;
  matched_count: number;
}
