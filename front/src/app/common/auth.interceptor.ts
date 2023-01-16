import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
} from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { environment } from 'src/environments/environment';
import { LoginService } from 'src/app/services/login.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private loginService: LoginService) {}

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<unknown>> {
    // add auth header with jwt if account is logged in and request is to the api url
    const isApiUrl = request.url.startsWith(environment.apiUrl);
    if (this.loginService.token && isApiUrl) {
      request = request.clone({
        setHeaders: {
          Authorization: `${this.loginService.token.token_type} ${this.loginService.token.access_token}`,
        },
      });
    }
    return next.handle(request).pipe(
      catchError((err) => {
        if ([401, 403].includes(err.status)) {
          // auto logout if 401 or 403 response returned from api
          this.loginService.logout();
        }

        const error = err.error?.message || err.statusText;
        console.error(err);
        return throwError(() => new Error(error));
      })
    );
  }
}
