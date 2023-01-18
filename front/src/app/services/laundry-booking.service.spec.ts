import { TestBed } from '@angular/core/testing';

import { LaundryBookingService } from './laundry-booking.service';

describe('LaundryBookingService', () => {
  let service: LaundryBookingService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LaundryBookingService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
