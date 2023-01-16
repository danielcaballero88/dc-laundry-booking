import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { LoginService } from 'src/app/services/login.service';
import { TokenStorageService } from 'src/app/services/token-storage.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  loginForm = new FormGroup({
    username: new FormControl(''),
    password: new FormControl(''),
  });

  @ViewChild('closeModal')
  closeModalRef!: ElementRef;

  isLoggedIn: boolean = false;


  constructor(public loginService: LoginService, private tokenStorageService: TokenStorageService) { }

  ngOnInit(): void {
    this.isLoggedIn = this.loginService.checkStatus();
  }

  login() {
    const username = this.loginForm.value.username
      ? this.loginForm.value.username
      : '';
    const password = this.loginForm.value.password
      ? this.loginForm.value.password
      : '';
    this.loginService.login(username, password);
    this.loginService.LoginSubject.subscribe({
      next: (data) => {
        // Close the dialog, the user is now logged in.
        console.log(data);
        console.log(this.closeModalRef);
        this.isLoggedIn = true;
        this.closeModalRef.nativeElement.click();
      },
      error: (err) => {
        console.error('Error loging in: ', err);
      },
      complete: () => {
        const savedToken = this.tokenStorageService.getToken();
        console.log("Login complete, savedToken: ", savedToken);
      }
    });
  }

  logout() {
    this.loginService.logout();
    this.isLoggedIn = false;
  }
}
