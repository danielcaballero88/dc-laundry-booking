export interface Token {
  access_token: string;
  token_type: string;
  expiration: number;
}

export interface User {
  username: string;
}

export interface WeekDatesSlots {
  [key: string]: { [key: number]: number };
}
