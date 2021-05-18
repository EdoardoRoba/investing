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
  chartDatasets: any //Array<any>=[]

  chartData: any
  chartLabels: any
  chartOptions = {
    responsive: true,
    animation: {
      duration: 0
    }
  };

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    interval(5000).subscribe(x => {this.getData()})
  }

  public chartClicked(e: any): void { }
  public chartHovered(e: any): void { }

  getData(){
    this.http.get(this.url+'history.json').subscribe((responseData:any) => {
      let temp : any[] = []
      Object.keys(responseData).forEach(element => {
        temp.push(responseData[element]);
      });
      console.log("finished",temp)
      this.chartData = [{data: temp.map( item => item.BTC ),label:"BTC"}]
      this.chartLabels = temp.map( item => item.date.replace("T"," ").slice(0,19) )
      // chart.update()
    });
  }

}
