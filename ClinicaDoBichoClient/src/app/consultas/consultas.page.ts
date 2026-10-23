import { Component, OnInit, inject, signal } from '@angular/core';
import { Consulta } from "../models/Consulta.model";
import { IonContent, IonHeader, IonTitle, IonItem, IonLabel, 
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
    IonContent, IonHeader, IonTitle, IonToolbar, IonList, IonItem,
    IonCard, IonCardHeader,IonCardSubtitle, IonCardTitle, IonCardContent
  ]
})

export class ConsultasPage implements OnInit {

  consultas = signal<Consulta[]>([]);
  private api = inject(ApiService)
  constructor() {}

  ngOnInit() {
      this.getConsultas(); 
  }

  getConsultas(){
   this.api.getConsultas()
           .subscribe(
              (data) =>{
                           this.consultas.set(data); 
                           console.log("consulta this.consultas", this.consultas())
                       },
              (err:Error) => console.error('Erro ao buscar consultas: ', err)
            )        
  }

}
