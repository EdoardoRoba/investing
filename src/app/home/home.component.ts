import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { interval } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { DialogComponent } from '../dialog/dialog.component';
import { CommunicationService } from '../services/communication.service/communication.service';

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
  dataToDisplay: any[]=[]
  dataToCheck: any[]=[]

  showLoading = true
  showEmptyMsg = false

  constructor(private http: HttpClient, private data: CommunicationService, public dialog: MatDialog) { }

  ngOnInit(): void {
    let tables: CryptoTemplate[]=[];
    this.data.currentMessage.subscribe(message => this.user = message)
    console.log("USR: ",this.user)
    // Retrieve the tables
    this.showLoading=true
    this.http.get(this.url+'tables.json').subscribe((responseData:any) => {
      Object.keys(responseData).forEach(element => {
        tables.push(responseData[element]);
      });
      console.log("data: ",tables)
      this.dataSource = tables
      console.log("keys: ",this.displayedColumns)
    });
    // Retrieve the data visible by the user
    this.http.get(this.url+'visibility/'+this.user+'.json').subscribe((responseData:any) => {
      // console.log("ciaoooo",responseData)
      this.dataToCheck = []
      Object.keys(responseData).forEach(element => {
        if (responseData[element] != this.user){
          this.dataToCheck.push(responseData[element]);
        }
      });
      this.fillDataToDisplay()
      this.showLoading=false
      if (this.dataToCheck.length===0){this.showLoading=false,this.showEmptyMsg=true}
      if (this.dataToCheck.length>0){this.showLoading=true,this.showEmptyMsg=false}

    });
    // this.http.get(this.url+'visibility/'+this.user+'.json').subscribe((responseData:any) => {
    //   // console.log("rgefedcf",responseData)
    //   Object.keys(responseData).forEach(element => {
    //     if (responseData[element] != this.user){
    //       this.dataToDisplay.push(responseData[element]);
    //     }
    //   });
    // });
    
    interval(5000).subscribe(x => {this.getData()})
    interval(5000).subscribe(x => {this.updateTableToDisplay()})
    interval(5000).subscribe(x => {this.fillDataToDisplay()})

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
        this.showEmptyMsg = false
        this.updateTableToDisplay()
      });
  }

  fillDataToDisplay(){
    // console.log("table",this.dataSource)
    this.dataToDisplay = []
    // console.log("tables:",this.dataSource)
    // console.log("usersdata:",this.dataToCheck)
    this.dataSource.forEach((elTable:any) => {
      this.dataToCheck.forEach((elUser:any) => {
        if (elTable.acronym == elUser.acronym){

          this.dataToDisplay.push({name:elTable.name,
                                  acronym:elTable.acronym,
                                  starting_price:elUser.starting_price,
                                  starting_price_usd:(elUser.starting_price*elUser.quantity).toFixed(2),
                                  quantity:elUser.quantity,
                                  date:elUser.date.substring(0,10),
                                  current_value:elTable.current_value,
                                  delta_position:0,
                                  selling_value:0,
                                  income:(0*elUser.quantity - elUser.starting_price*elUser.quantity).toFixed(2),
                                  position:(elTable.current_value*elUser.quantity-elUser.starting_price*elUser.quantity).toFixed(2),
                                  current_position:(elTable.current_value*elUser.quantity-elUser.starting_price*elUser.quantity).toFixed(2)
                                })
        }
      })
    });
    // console.log("dataaaa",this.dataToDisplay)
  }

  updateTableToDisplay(){
    // this.showLoading=true
    this.http.get(this.url+'visibility/'+this.user+'.json').subscribe((responseData:any) => {
      this.dataToCheck = []
      Object.keys(responseData).forEach(element => {
        if (responseData[element] != this.user){
          this.dataToCheck.push(responseData[element]);
        }
      });
      this.fillDataToDisplay()
      this.showLoading=false
      if (this.dataToCheck.length===0){this.showLoading=false,this.showEmptyMsg=true}
      if (this.dataToCheck.length>0){this.showLoading=true,this.showEmptyMsg=false}
    });
  }

}
