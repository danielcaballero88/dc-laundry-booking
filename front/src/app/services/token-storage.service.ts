import { Injectable } from '@angular/core';
import { Token, User } from 'src/app/models/shared';

const TOKEN_KEY = 'auth-token';
const USER_KEY = 'auth-user';

@Injectable({
  providedIn: 'root'
})
export class TokenStorageService {
  constructor() { }

  clearStorage(): void {
    window.sessionStorage.clear();
  }

  public saveToken(token: Token): void {
    window.sessionStorage.removeItem(TOKEN_KEY);
    window.sessionStorage.setItem(TOKEN_KEY, JSON.stringify(token));
  }

  public getToken(): Token | null {
    const storedToken = window.sessionStorage.getItem(TOKEN_KEY);
    const token: Token | null = storedToken ? JSON.parse(storedToken) : null;
    return token;
  }

  public saveUser(user: User): void {
    window.sessionStorage.removeItem(USER_KEY);
    window.sessionStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  public getUser(): User | null {
    const storedUser = window.sessionStorage.getItem(USER_KEY);
    const user: User | null = storedUser ? JSON.parse(storedUser) : null;
    return user;
  }
}
