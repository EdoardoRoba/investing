import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-dialog',
  templateUrl: './dialog.component.html',
  styleUrls: ['./dialog.component.css']
})
export class DialogComponent implements OnInit {

  name = ""
  acronym = ""
  quantity: number=0
  date = new Date()

  constructor(private http: HttpClient,@Inject(MAT_DIALOG_DATA) public user: any) { }

  ngOnInit(): void {
  }

  addCrypto(){
    
  }

}
