import { Component, OnInit, inject } from '@angular/core';
import { Consulta } from "../models/Consulta.model";
import { IonContent, IonHeader, IonTitle, IonItem, IonLabel, IonInput,
         IonToolbar, IonButton, IonList, 
         IonCard, IonCardHeader,IonCardSubtitle, IonCardTitle, IonCardContent } from '@ionic/angular';
import { ApiService } from "../services/api.service";
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-consultas',
  templateUrl: './consultas.page.html',
  styleUrls: ['./consultas.page.scss'],
  standalone: true,
  imports:[
    CommonModule,
    IonContent, IonHeader, IonTitle, IonToolbar, IonList, 
    IonCard, IonCardHeader,IonCardSubtitle, IonCardTitle, IonCardContent
  ]
})
export class ConsultasPage implements OnInit {

  consultas : Consulta[]=[];
  private api = inject(ApiService)
  constructor() { }

  ngOnInit() {
    this.getConsultas();
  }

  getConsultas(){
   this.api.getConsultas()
            .subscribe(
              (data:Consulta[]) => {this.consultas = data; console.log("consulta",data)},
              err => console.error('Erro ao buscar consultas: ', err)
            )
            
  }

}
