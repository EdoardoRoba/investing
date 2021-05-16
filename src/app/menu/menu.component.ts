import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

export interface Tile {
  color: string;
  cols: number;
  rows: number;
  text: string;
  icon: string
}

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css'],
})
export class MenuComponent implements OnInit {

  tiles: Tile[] = [
    {text: 'Your cryptos', cols: 3, rows: 1, color: 'lightblue', icon: 'home'},
    {text: 'History', cols: 1, rows: 2, color: 'lightgreen', icon: 'timeline'},
    {text: 'Buy/Sell', cols: 1, rows: 1, color: 'lightpink', icon: 'swap_vert'},
    {text: 'You', cols: 2, rows: 1, color: '#DDBDF1', icon: 'account_circle'},
  ];

  constructor(private router: Router) {}

  ngOnInit(): void {}

  goTo(toPage: string){
    if (toPage=='Your cryptos'){
      toPage = 'Home'
    }
    if (toPage=='Buy/Sell'){
      toPage = 'buysell'
    }
    this.router.navigateByUrl('/'+toPage.toLowerCase());
  }

}
