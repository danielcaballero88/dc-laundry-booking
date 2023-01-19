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

  constructor(
    private loginService: LoginService,
    private tokenStorageService: TokenStorageService,
  ) {}

  ngOnInit(): void {
    // Get initial logged in status.
    this.isLoggedIn = this.loginService.checkStatus();

    // Listen for loggin and logout events.
    this.loginService.LoginSubject.subscribe({
      next: (data) => {
        // Close the dialog, the user is now logged in.
        console.log('Success logging in: ', data);
        this.isLoggedIn = true;
        this.closeModalRef.nativeElement.click();
      },
      error: (err) => {
        console.error('Error logging in: ', err);
      },
    });

    this.loginService.LoginErrorSubject.subscribe({
      next: () => {
        console.log('Logging failed.');
      },
    });

    this.loginService.LogoutSubject.subscribe({
      next: () => {
        this.isLoggedIn = false;
      },
    });
  }

  login() {
    const username = this.loginForm.value.username
      ? this.loginForm.value.username
      : '';
    const password = this.loginForm.value.password
      ? this.loginForm.value.password
      : '';
    this.loginService.login(username, password);
  }

  logout() {
    this.loginService.logout();
  }
}
