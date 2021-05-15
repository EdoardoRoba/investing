import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

export interface Tile {
  color: string;
  cols: number;
  rows: number;
  text: string;
}

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css'],
})
export class MenuComponent implements OnInit {

  tiles: Tile[] = [
    {text: 'Home', cols: 3, rows: 1, color: 'lightblue'},
    {text: 'History', cols: 1, rows: 2, color: 'lightgreen'},
    {text: 'Buy/Sell', cols: 1, rows: 1, color: 'lightpink'},
    {text: 'You', cols: 2, rows: 1, color: '#DDBDF1'},
  ];

  constructor(private router: Router) {}

  ngOnInit(): void {}

  goTo(toPage: string){
    this.router.navigateByUrl('/'+toPage.toLowerCase());
  }

}
