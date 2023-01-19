import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-booking-slot',
  templateUrl: './booking-slot.component.html',
  styleUrls: ['./booking-slot.component.scss'],
})
export class BookingSlotComponent implements OnInit {
  @Input()
  status: number = 0;

  constructor() {}

  ngOnInit(): void {}

  temp(val: any): string {
    return typeof val;
  }
}
