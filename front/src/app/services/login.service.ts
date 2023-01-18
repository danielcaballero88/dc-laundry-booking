import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, OnInit } from '@angular/core';
import { Subject } from 'rxjs';

import { Token, User } from 'src/app/models/shared';
import { TokenStorageService } from 'src/app/services/token-storage.service';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class LoginService implements OnInit {
  LoginSubject = new Subject<{user: User, token: Token}>();
  LogoutSubject = new Subject<void>();
  token: Token | null = null;
  user: User | null = null;

  constructor(
    private http: HttpClient,
    private tokenStorageService: TokenStorageService
  ) { }

  ngOnInit(): void {
    this.token = this.tokenStorageService.getToken();
    this.user = this.tokenStorageService.getUser();
  }

  checkStatus(): boolean {
    this.user = this.tokenStorageService.getUser();
    this.token = this.tokenStorageService.getToken();
    if (this.user && this.token) {
      return true;
    }
    return false;
  }

  login(username: string, password: string) {
    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded',
    });

    const body = new URLSearchParams();
    body.set('username', username);
    body.set('password', password);

    this.http
      .post<Token>(environment.apiUrl + '/auth/login', body.toString(), {
        headers: headers,
        withCredentials: true,
      })
      .subscribe({
        next: (tokenObj: Token) => {
          // Create user object and store it.
          const userObj = {username};
          this.tokenStorageService.saveUser(userObj);
          this.user = userObj;
          // Also store the token object.
          this.token = tokenObj;
          this.tokenStorageService.saveToken(tokenObj);
          // And push the references to the login subject.
          this.LoginSubject.next({user: this.user, token: this.token});
        },
        error: (err) => {
          this.LoginSubject.error(err);
        },
        complete: () => {
          this.LoginSubject.complete();
        },
      });
  }

  logout() {
    console.log("Logging out, clearing storage.");
    this.tokenStorageService.clearStorage();
    this.token = null;
    this.user = null;
    this.LogoutSubject.next();
  }
}
