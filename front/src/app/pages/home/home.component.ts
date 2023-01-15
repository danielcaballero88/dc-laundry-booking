import { Component, OnInit } from '@angular/core';

interface TableData {
  [key: string]: { [key: number]: number };
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  slotsData = {
    0: {startHour: 7, endHour: 10},
    1: {startHour: 10, endHour: 13},
    2: {startHour: 13, endHour: 16},
    3: {startHour: 16, endHour: 19},
    4: {startHour: 19, endHour: 22},
  };

  tableData: TableData = {
    '2023/01/16': { 0: 0, 1: 2, 2: 4, 3: 6, 4: 8 },
    '2023/01/17': { 0: 0, 1: 2, 2: 4, 3: 6, 4: 8 },
    '2023/01/18': { 0: 0, 1: 2, 2: 4, 3: 6, 4: 8 },
    '2023/01/19': { 0: 0, 1: 2, 2: 4, 3: 6, 4: 8 },
    '2023/01/20': { 0: 0, 1: 2, 2: 4, 3: 6, 4: 8 },
    '2023/01/21': { 0: 0, 1: 2, 2: 4, 3: 6, 4: 8 },
    '2023/01/22': { 0: 0, 1: 2, 2: 4, 3: 6, 4: 8 },
  };

  constructor() {}

  ngOnInit(): void {}

  getCellData(dateStr: string, slotIdStr: string) {
    const slotId = Number(slotIdStr);
    return this.tableData[dateStr][slotId];
  }
}
