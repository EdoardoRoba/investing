import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { WavesModule } from 'angular-bootstrap-md'
import { interval } from 'rxjs';
import { ChartsModule } from 'ng2-charts';
// import { multi } from './data';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {

  url = 'https://investing-82e20-default-rtdb.firebaseio.com/investing/'
  chartDatasets: any //Array<any>=[]
  chartLabels: any

  // multi: any[]=[] //Number[]=[] //=[Number,Number];
  // view = [700, 300];
  // legend: boolean = true;
  // showLabels: boolean = true;
  // animations: boolean = true;
  // xAxis: boolean = true;
  // yAxis: boolean = true;
  // showYAxisLabel: boolean = true;
  // showXAxisLabel: boolean = true;
  // xAxisLabel: string = 'Year';
  // yAxisLabel: string = 'Population';
  // timeline: boolean = true;

  // colorScheme = {
  //   domain: ['#5AA454'] //, '#E44D25', '#CFC0BB', '#7aa3e5', '#a8385d', '#aae3f5']
  // };

  constructor(private http: HttpClient) {
    // Object.assign(this, { multi });
  }

  ngOnInit(): void {
    interval(5000).subscribe(x => {this.getData()})
  }

  public chartType: string = 'line';

  // public chartDatasets: Array<any> = [
  //   { data: [65, 59, 80, 81, 56, 55, 40], label: 'My First dataset' },
  //   { data: [28, 48, 40, 19, 86, 27, 90], label: 'My Second dataset' }
  // ];

  // public chartLabels: Array<any> = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

  public chartColors: Array<any> = [
    {
      backgroundColor: 'rgba(105, 0, 132, .2)',
      borderColor: 'rgba(200, 99, 132, .7)',
      borderWidth: 2,
    },
    {
      backgroundColor: 'rgba(0, 137, 132, .2)',
      borderColor: 'rgba(0, 10, 130, .7)',
      borderWidth: 2,
    }
  ];

  public chartOptions: any = {
    responsive: true
  };

  public chartClicked(e: any): void { }
  public chartHovered(e: any): void { }

  getData(){
    this.http.get(this.url+'history.json').subscribe((responseData:any) => {
      let temp : any[] = []
      Object.keys(responseData).forEach(element => {
        temp.push(responseData[element]);
      });
      console.log("finished",temp)
      // this.chartDatasets = Array.assign({}, ...temp.map((x) => ({[x.date]: x.BTC})));
      this.chartDatasets = {data: temp.map( item => item.BTC ),label:"BTC"}
      console.log("finished DIC",this.chartDatasets)
      this.chartLabels = temp.map( item => item.date )
      // this.chartLabels = Object.assign({}, ...temp.map((x) => ({[x.date]: x.date})));
      console.log("finished DIC",this.chartLabels)
      // this.multi = this.chartDatasets
      // console.log(this.multi)
      // this.chartDatasets = responseData
      // console.log("first historyyyyyyy",this.chartDatasets)
    });
  }

  // onSelect(data:any): void {
  //   console.log('Item clicked', JSON.parse(JSON.stringify(data)));
  // }

  // onActivate(data:any): void {
  //   console.log('Activate', JSON.parse(JSON.stringify(data)));
  // }

  // onDeactivate(data:any): void {
  //   console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  // }

}
