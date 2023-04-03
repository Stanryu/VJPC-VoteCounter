<template>
    <div class="container">
		<div class="jumbotron vertical-center">
			
			<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css" 
			integrity="sha384-9+PGKSqjRdkeAU7Eu4nkJU8RFaH8ace8HGXnkiKMP9I9Te0GJ4/km3L1Z8tXigpG" crossorigin="anonymous">
			
			<div class="row">
				<div class="col-sm-12">
					<h2 class="text-center bg-primary text-white">Set Up an Election</h2>
					<hr><br>
					
					<b-alert variant="success" v-if="showMessage" show fade dismissible>{{ message }}</b-alert>
					<br>
					
					<button type="button" class="btn btn-success btn-sm" v-b-modal.election-modal>Create Election</button>
					<br><br>
					
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
						<tbody>
							<tr v-for="election, index in elections" :key="index">
								<td>{{ election.Name }}</td>
								<td>{{ election.Description }}</td>
								<td>{{ election.Quantity }}</td>
								<td>{{ election.StartDate }} {{ election.StartTime }}</td>
								<td>{{ election.EndDate }} {{ election.EndTime }}</td>
								<td>{{ election.Fingerprint }}</td>
								<td>
									<div class="btn-group" role="group">
										<button type="button" class="btn btn-info btn-sm" v-b-modal.election-edit-modal @click="editElection(election)">Update</button>
										<button type="button" class="btn btn-danger btn-sm" @click="deleteElection(election)">Delete</button>
									</div>
								</td>
							</tr>
						</tbody>
					</table>
					<footer class="bg-primary text-white text-center" style="border-radius: 10px;">Copyright &copy;. All Rights Reserved 2023.</footer>
				</div>
			</div>

			<b-modal ref="createElectionModal" id="election-modal" title="Create a New Election" hide-backdrop hide-footer>
				<b-form @submit="onSubmit" @reset="onReset" class="w-100 text-center">
					<b-form-group id="form-name-group" label="Name" label-for="form-name-input">
						<b-form-input id="form-name-input" 
									type="text" 
									v-model="createElectionForm.Name" 
									required 
									placeholder="Enter the election name...">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-description-group" label="Description" label-for="form-description-input">
						<b-form-input id="form-description-input" 
									type="text" 
									v-model="createElectionForm.Description" 
									required 
									placeholder="Enter the election description...">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-Quantity-group" label="Quantity" label-for="form-Quantity-input">
						<b-form-input id="form-Quantity-input" 
									type="text" 
									v-model="createElectionForm.Quantity" 
									required 
									placeholder="Enter the number of positions...">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-begindate-group" label="Start Date" label-for="form-begindate-input">
						<b-form-input id="form-begindate-input" 
									type="text" 
									v-model="createElectionForm.StartDate" 
									required 
									placeholder="Enter the election start date... (e.g., dd/MM/yyyy)">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-starttime-group" label="Start Time" label-for="form-starttime-input">
						<b-form-input id="form-starttime-input" 
									type="text" 
									v-model="createElectionForm.StartTime" 
									required 
									placeholder="Enter the election start time... (e.g., hh:mm)">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-enddate-group" label="End Date" label-for="form-enddate-input">
						<b-form-input id="form-enddate-input" 
									type="text" 
									v-model="createElectionForm.EndDate" 
									required 
									placeholder="Enter the election end date... (e.g., dd/MM/yyyy)">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-endtime-group" label="End Time" label-for="form-endtime-input">
						<b-form-input id="form-endtime-input" 
									type="text" 
									v-model="createElectionForm.EndTime" 
									required 
									placeholder="Enter the election end time... (e.g., hh:mm)">
						</b-form-input>
					</b-form-group>
					
					<!-- Cargos -> nome e dígitos -->

					<b-form-group id="form-candidatesfile-group" label="Candidates File" label-for="form-candidatesfile-input">
						<b-form-input id="form-candidatesfile-input" 
									type="text" 
									v-model="createElectionForm.CandidatesFile" 
									required 
									placeholder="Enter the candidates file name... ">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-votersfile-group" label="Voters File" label-for="form-votersfile-input">
						<b-form-input id="form-votersfile-input" 
									type="text" 
									v-model="createElectionForm.VotersFile" 
									required 
									placeholder="Enter the voters file name... ">
						</b-form-input>
					</b-form-group>

					<b-button type="submit" variant="outline-info">Submit</b-button>
					<b-button type="reset" variant="outline-danger">Reset</b-button>
				</b-form>
			</b-modal>

			<b-modal ref="editElectionModal" id="election-edit-modal" title="Edit an Election" hide-backdrop hide-footer>
				<b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100 text-center">
					
					<b-form-group id="form-name-edit-group" label="Name" label-for="form-name-edit-input">
						<b-form-input id="form-name-edit-input" 
									type="text" 
									v-model="editElectionForm.Name" 
									required 
									placeholder="Enter the election name...">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-description-edit-group" label="Description" label-for="form-description-edit-input">
						<b-form-input id="form-description-edit-input" 
									type="text" 
									v-model="editElectionForm.Description" 
									required 
									placeholder="Enter the election description...">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-quantity-edit-group" label="Quantity" label-for="form-quantity-edit-input">
						<b-form-input id="form-quantity-edit-input" 
									type="text" 
									v-model="editElectionForm.Quantity" 
									required 
									placeholder="Enter the number of positions...">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-begindate-edit-group" label="Start Date" label-for="form-begindate-edit-input">
						<b-form-input id="form-begindate-edit-input" 
									type="text" 
									v-model="editElectionForm.StartDate" 
									required 
									placeholder="Enter the election start date... (e.g., dd/MM/yyyy)">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-starttime-edit-group" label="Start Time" label-for="form-starttime-edit-input">
						<b-form-input id="form-starttime-edit-input" 
									type="text" 
									v-model="editElectionForm.StartTime" 
									required 
									placeholder="Enter the election start time... (e.g., hh:mm)">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-enddate-edit-group" label="End Date" label-for="form-enddate-edit-input">
						<b-form-input id="form-enddate-edit-input" 
									type="text" 
									v-model="editElectionForm.EndDate" 
									required 
									placeholder="Enter the election end date... (e.g., dd/MM/yyyy)">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-endtime-edit-group" label="End Time" label-for="form-endtime-edit-input">
						<b-form-input id="form-endtime-edit-input" 
									type="text" 
									v-model="editElectionForm.EndTime" 
									required 
									placeholder="Enter the election end time... (e.g., hh:mm)">
						</b-form-input>
					</b-form-group>
					
					<!-- Cargos -> nome e dígitos -->

					<b-form-group id="form-candidatesfile-edit-group" label="Candidates File" label-for="form-candidatesfile-edit-input">
						<b-form-input id="form-candidatesfile-edit-input" 
									type="text" 
									v-model="editElectionForm.CandidatesFile" 
									required 
									placeholder="Enter the candidates file name... ">
						</b-form-input>
					</b-form-group>

					<b-form-group id="form-votersfile-edit-group" label="Voters File" label-for="form-votersfile-edit-input">
						<b-form-input id="form-votersfile-edit-input" 
									type="text" 
									v-model="editElectionForm.VotersFile" 
									required 
									placeholder="Enter the voters file name... ">
						</b-form-input>
					</b-form-group>

					<b-button type="submit" variant="outline-info">Submit</b-button>
					<b-button type="reset" variant="outline-danger">Reset</b-button>
				</b-form>
			</b-modal>
		</div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			elections: [],
			createElectionForm: {
				'Name': '',
				'Description': '',
				'Quantity': '',
				'StartDate': '',
				'StartTime': '',
				'EndDate': '',
				'EndTime': '',
				'CandidatesFile': '',
				'VotersFile': ''
			},
			editElectionForm: {
				'ID': '',
				'Name': '',
				'Description': '',
				'Quantity': '',
				'StartDate': '',
				'StartTime': '',
				'EndDate': '',
				'EndTime': '',
				'CandidatesFile': '',
				'VotersFile': ''
			}
		};
	},
	message: '',
	methods: {
		getElections() {
			const path = 'http://localhost:5000';
			axios.get(path)
			.then((res) => {
				this.elections = res.data.elections;
			})
			.catch((err) => {
				alert(err);
			});
		},
		createElection(payload) {
			const path = 'http://localhost:5000';
			axios.post(path, payload)
			.then(() => {
				this.getElections();
				this.message = 'Election Created!';
				this.showMessage = true;
			})
			.catch((err) => {
				alert(err);
				this.getElections();
			});
		},
		clearForm() {
			this.createElectionForm.Name = '',
			this.createElectionForm.Description = '',
			this.createElectionForm.Quantity = '',
			this.createElectionForm.StartDate = '',
			this.createElectionForm.StartTime = '',
			this.createElectionForm.EndDate = '',
			this.createElectionForm.EndTime = ''
			this.createElectionForm.CandidatesFile = '',
			this.createElectionForm.VotersFile = ''
			this.editElectionForm.ID = '',
			this.editElectionForm.Name = '',
			this.editElectionForm.Description = '',
			this.editElectionForm.Quantity = '',
			this.editElectionForm.StartDate = '',
			this.editElectionForm.StartTime = '',
			this.editElectionForm.EndDate = '',
			this.editElectionForm.EndTime = ''
			this.editElectionForm.CandidatesFile = '',
			this.editElectionForm.VotersFile = ''
		},
		onSubmit(e) {
			e.preventDefault();
			this.$refs.createElectionModal.hide();
			const payload = {
				Name: this.createElectionForm.Name,
				Description: this.createElectionForm.Description,
				Quantity: this.createElectionForm.Quantity,
				StartDate: this.createElectionForm.StartDate,
				StartTime: this.createElectionForm.StartTime,
				EndDate: this.createElectionForm.EndDate,
				EndTime: this.createElectionForm.EndTime,
				CandidatesFile: this.createElectionForm.CandidatesFile,
				VotersFile: this.createElectionForm.VotersFile
			};
			this.createElection(payload);
			this.clearForm();
		},
		onReset(e) {
			e.preventDefault();
			this.$refs.createElectionModal.hide();
			this.clearForm();
		},
		onSubmitUpdate(e) {
			e.preventDefault();
			this.$refs.editElectionModal.hide();
			const payload = {
				Name: this.editElectionForm.Name,
				Description: this.editElectionForm.Description,
				Quantity: this.editElectionForm.Quantity,
				StartDate: this.editElectionForm.StartDate,
				StartTime: this.editElectionForm.StartTime,
				EndDate: this.editElectionForm.EndDate,
				EndTime: this.editElectionForm.EndTime,
				CandidatesFile: this.editElectionForm.CandidatesFile,
				VotersFile: this.editElectionForm.VotersFile
			};
			this.updateElection(payload, this.editElectionForm.ID);
			this.clearForm();
		},
		onResetUpdate(e) {
			e.preventDefault();
			this.$refs.editElectionModal.hide();
			this.clearForm();
			this.getElections();
		},
		updateElection(payload, electionID) {
			const path = `http://localhost:5000/${electionID}`;
			axios.put(path, payload)
			.then(() => {
				this.getElections();
				this.message = 'Election Updated!';
				this.showMessage = true;
			})
			.catch((err) => {
				alert(err);
				this.getElections();
			});
		},
		editElection(election) {
			this.editElectionForm = election;
		},
		removeElection(electionID) {
			const path = `http://localhost:5000/${electionID}`;
			axios.delete(path)
			.then(() => {
				this.getElections();
				this.message = 'Election Removed!';
				this.showMessage = true;
			})
			.catch((err) => {
				alert(err);
				this.getElections();
			});
		},
		deleteElection(election) {
			this.removeElection(election.ID);
		}
	},
	created() {
		this.getElections();
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h2 {
	padding: 15px;
	border-radius: 10px;
}
h3 {
  margin: 40px 0 0;
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
</style>
