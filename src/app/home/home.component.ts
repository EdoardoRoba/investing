import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { CommunicationService } from '../communication.service';

export interface CryptoTemplate {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  user = ""
  url = 'https://investing-82e20-default-rtdb.firebaseio.com/investing/cryptos.json'
  cryptos: any[]=[];

  constructor(private http: HttpClient, private data: CommunicationService) { }

  ngOnInit(): void {
    this.data.currentMessage.subscribe(message => this.user = message)
    console.log("USR: ",this.user)
    this.http.get(this.url).subscribe((responseData:any) => {
      Object.keys(responseData).forEach(element => {
        this.cryptos.push(responseData[element]);
      });
      console.log("data: ",this.cryptos)
    });
  }

}
