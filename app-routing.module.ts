import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LoginComponent } from './login/login.component';
import { PredictionComponent } from './prediction/prediction.component';

const routes: Routes = [{path:'',component:LoginComponent},
{path:'dashboard',component:DashboardComponent},
{path:'prediction',component:PredictionComponent}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
