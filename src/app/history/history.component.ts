import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { WavesModule } from 'angular-bootstrap-md'
import { interval } from 'rxjs';
import { ChartDataSets, ChartOptions, ChartType } from 'chart.js';
// import { Color, BaseChartDirective, Label } from 'ng2-charts';
// import * as pluginAnnotations from 'chartjs-plugin-annotation';
// import { multi } from './data';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {

  url = 'https://investing-82e20-default-rtdb.firebaseio.com/investing/'
  filterOnCrypto = ""
  allCryptos: any[]=[]
  oneMonth = 2592000000

  datesWindow = [
    {
      label: "last hour",
      value: 3600000
    },
    {
      label: "last 24 hours",
      value: 86400000
    },
    {
      label: "last two days",
      value: 172800000
    },
    {
      label: "last week",
      value: 604800000
    },
    {
      label: "last month",
      value: 2592000000
    }
  ]

  dateWindow = 0

  chartDatasets: any //Array<any>=[]
  chartData: any
  chartLabels: any
  chartOptions = {
    responsive: true,
    animation: {
      duration: 0
    } //,
    // scales : {
    //   yAxes: [{
    //      ticks: {
    //         steps : 1000,
    //         stepValue : 1000,
    //         max : 45000,
    //         min: 40000
    //       }
    //   }]
    // }
  };

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get(this.url+'tables.json').subscribe((responseData:any) => {
      Object.keys(responseData).forEach(element => {
        this.allCryptos.push({name:responseData[element].name,acronym:responseData[element].acronym})
      });
      // console.log("all",this.allCryptos)
    })
    
    interval(5000).subscribe(x => {this.getData()})
    interval(50000).subscribe(x => {this.limitData()})
  }

  public chartClicked(e: any): void { }
  public chartHovered(e: any): void { }

  getData(){
    // console.log("ehi",this.filterOnCrypto)
    if (this.filterOnCrypto!==""){
      this.http.get(this.url+'history.json').subscribe((responseData:any) => {
        let temp : any[] = []
        Object.keys(responseData).forEach(element => {
          temp.push(responseData[element]);
        });
        // console.log("temp",temp)
        let d = new Date()
        // this.chartData = [{data: temp.map( item => item.BTC ),label:this.filterOnCrypto}]
        this.chartData = [{data: temp.map( item => {
          if (d.valueOf()-new Date(item.date).valueOf() < this.dateWindow){ // a month: 2592000000 ms
            return item[this.filterOnCrypto]
          } else {
            return -1
          }
        }),label:this.filterOnCrypto}]
        this.chartData[0]["data"] = this.chartData[0]["data"].filter((el:any)=>el !== -1)
        // this.chartLabels = [{data: temp.map( item => item.date.replace("T"," ").slice(0,19) ),label:this.filterOnCrypto}]
        this.chartLabels = temp.map(item => {
          if(d.valueOf()-new Date(item.date).valueOf() < this.dateWindow){ // un'ora e mezza: 4500000
            return item.date.replace("T"," ").slice(0,19)
          } else{
            return -1
          }
        })
        this.chartLabels = this.chartLabels.filter((el:any)=>el !== -1)
        // chart.update()
      });
    }
  }

  limitData(){
    let dataLimited: any[]=[]
    let d = new Date()
    this.http.get(this.url+'history.json').subscribe((responseData:any) => {
      Object.keys(responseData).forEach((element:any) => {
        if (d.valueOf()-new Date(responseData[element].date).valueOf()<=this.oneMonth){
          dataLimited.push(responseData[element])
        }
      });
      this.http.put(this.url+'history.json',dataLimited).subscribe()
    })
  }

}
