import { inject, Service } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Consulta } from "../models/Consulta.model";

const URL_DJANGO =  'http://127.0.0.1:8000/api'; // backend Django

@Service()
export class ApiService {

    private http= inject(HttpClient);

    login(username:string, password:string):Observable<any>{
        return this.http.post(`${URL_DJANGO}/login/`, {username, password});
    }

    getConsultas():Observable<Consulta[]>{
        return this.http.get<Consulta[]>(`${URL_DJANGO}/consultas/`);
    }

    agendarConsulta(consulta:Consulta):Observable<Consulta>{
        return this.http.post<Consulta>(`${URL_DJANGO}/consultas/`, consulta);
    }
}
