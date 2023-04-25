<template>
    <div class="container">
		<div class="jumbotron vertical-center">
			
			<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css" 
			integrity="sha384-9+PGKSqjRdkeAU7Eu4nkJU8RFaH8ace8HGXnkiKMP9I9Te0GJ4/km3L1Z8tXigpG" crossorigin="anonymous">
			
			<!-- Election Configuration Main Page -->
			<div class="row">
				<div class="col-sm-12">
					<h2 class="text-center bg-primary text-white">Totalization</h2>

					<!-- Contens of Each Election Displayed on a Table Format -->
					<table class="table table-hover">
						<thead>
							<tr>
								<th scope="col">Name</th>
								<th scope="col">Description</th>
								<th scope="col">Number of Positions</th>
								<th scope="col">Begins</th>
								<th scope="col">Ends</th>
								<th scope="col">Fingerprint</th>
								<th scope="col">Actions</th>
							</tr>
						</thead>
						<tbody v-for="election, index in elections" :key="index">
							<tr v-if="closed(election)">
								<td>{{ election.Name }}</td>
								<td>{{ election.Description }}</td>
								<td>{{ election.Quantity }}</td>
								<td>{{ election.StartDate }}<br>{{ election.StartTime }}</td>
								<td>{{ election.EndDate }}<br>{{ election.EndTime }}</td>
								<td>{{ election.Fingerprint }}</td>
								<td>
									<div class="btn-group" role="group"> 
										<button type="button" class="btn btn-dark btn-sm" 
										:disabled="isManageable(election)" @click="tallyElection(election)">Tally</button>
										<button type="button" class="btn btn-info btn-sm" 
										:disabled="isManageable(election)" @click="tallyElection(election)">Video</button>
									</div>
								</td>
							</tr>
						</tbody>
					</table>
					<footer class="bg-primary text-white text-center" style="border-radius: 10px;">
						Copyright &copy;. All Rights Reserved 2023.
					</footer>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			elections: []
		};
	},
	
	methods: {
		getElections() {
			const path = 'http://localhost:5000/totalization';
			axios.get(path)
			.then((res) => {
				this.elections = res.data.elections;
			})
			.catch((err) => {
				alert(err);
			});
		},
		
		closed(election) {

			let end = election.EndDate.split('/')
			let endDate = `${end[2]}-${end[1]}-${end[0]}T${election.EndTime}`;

			if (new Date(endDate) < new Date()) 
				return true;
			else 
				return false;
		},

		isManageable(election) {

			let splitDate = election.EndDate.split('/')
			let formattedDate = `${splitDate[2]}-${splitDate[1]}-${splitDate[0]}T${election.EndTime}`;

			if (new Date(formattedDate) >= new Date()) 
				return true;
			else 
				return false;
		}
	},
	created() {
		this.getElections();
	}

}
</script>

<style scoped>
h2 {
	padding: 15px;
	border-radius: 10px;
}
h3 {
	margin: 0 auto;
	padding: 10px;
	width: 20%;
	border-radius: 5px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.jumbotron {
	position: absolute;
	width: 90%;
	left: 5%;
}
</style>