import { Component, Input, OnInit } from '@angular/core';
import { SlotObj } from 'src/app/models/shared';
import { LaundryBookingService } from 'src/app/services/laundry-booking.service';

@Component({
  selector: 'app-booking-slot',
  templateUrl: './booking-slot.component.html',
  styleUrls: ['./booking-slot.component.scss'],
})
export class BookingSlotComponent implements OnInit {
  @Input()
  slotObj!: SlotObj;

  constructor(private laundryBookingService: LaundryBookingService) {}

  ngOnInit(): void {}

  bookSlot() {
    this.laundryBookingService
      .bookSlot(this.slotObj.date, this.slotObj.id)
      .subscribe({
        next: (data) => {
          console.log('Success: ', data);
          this.slotObj.status = 3;
        },
        error: (err) => {
          console.error('Error: ', err);
        },
      });
  }

  unbookSlot() {
    this.laundryBookingService
      .unbookSlot(this.slotObj.date, this.slotObj.id)
      .subscribe({
        next: (data) => {
          console.log('Success: ', data);
          this.slotObj.status = 1;
        },
        error: (err) => {
          console.error('Error: ', err);
        },
      });
  }
}
