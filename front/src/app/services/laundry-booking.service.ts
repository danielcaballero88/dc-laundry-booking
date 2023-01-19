import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { WeekDatesSlots } from 'src/app/models/shared';

@Injectable({
  providedIn: 'root',
})
export class LaundryBookingService {
  constructor(private http: HttpClient) {}

  getWeek(offset: number) {
    const queryParams = new HttpParams().set('offset', offset);
    return this.http.get<WeekDatesSlots>(
      environment.apiUrl + '/booking/getweek',
      { params: queryParams },
    );
  }
}
