import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { CommunicationService } from '../communication.service';
import { interval } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { DialogComponent } from '../dialog/dialog.component';

export interface CryptoTemplate {
  name: string;
  acronym: string;
  starting_price: number;
  starting_price_usd: number;
  quantity: number;
  date: Date;
  current_value: number;
  delta_position: number;
  selling_value: number;
  income: number;
  position: number;
  current_position: number;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  user = ""
  url = 'https://investing-82e20-default-rtdb.firebaseio.com/investing/'
  displayedColumns: string[] = ["name","acronym","starting_price","starting_price_usd","quantity","date",
                                "current_value","delta_position","selling_value","income","position","current_position"]
  dataSource: any

  constructor(private http: HttpClient, private data: CommunicationService, public dialog: MatDialog) { }

  ngOnInit(): void {
    let tables: CryptoTemplate[]=[];
    this.data.currentMessage.subscribe(message => this.user = message)
    console.log("USR: ",this.user)
    this.http.get(this.url+'tables.json').subscribe((responseData:any) => {
      Object.keys(responseData).forEach(element => {
        tables.push(responseData[element]);
      });
      console.log("data: ",tables)
      this.dataSource = tables
      console.log("keys: ",this.displayedColumns)
    });
    interval(5000).subscribe(x => {this.getData()})
  }

  getData(){
    let tables: CryptoTemplate[]=[];
    this.data.currentMessage.subscribe(message => this.user = message)
    // console.log(Date.now())
    // console.log("USR: ",this.user)
    this.http.get(this.url+'tables.json').subscribe((responseData:any) => {
      Object.keys(responseData).forEach(element => {
        tables.push(responseData[element]);
      });
      this.dataSource = tables
      // console.log("data222: ",tables)
      // console.log("keys: ",this.displayedColumns)
    });
  }

  addCrypto(){
    //Inject the data in the dialog
    const dialogRef = this.dialog.open(DialogComponent,{
      data: this.user
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
      // this.retrievedData = []
    });
  }

}
