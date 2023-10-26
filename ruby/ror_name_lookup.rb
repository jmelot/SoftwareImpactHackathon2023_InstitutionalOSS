#!/usr/bin/env ruby

require 'bundler/setup'
require 'http'
require 'active_support/all'
require 'csv'
require 'byebug'

in_file = ARGV[0]

# This is a bit hacky, but it's a simple self contained script at the moment.
# read the json and find the preferred name and ror id that matches best.
# Returns the proposed name and ror id {proposed: 'name', ror_id: 'id'}
def find_best_result(response:)
  hash = response.parse.with_indifferent_access
  return {proposed: '', ror_id: ''} if hash[:number_of_results] < 1

  rors = hash[:items].map(&:with_indifferent_access)
  ror = rors.select{ |i| i[:chosen] == true }.first

  # I believe it sorts by best matches first
  ror = rors.first if ror.nil?

  { proposed: ror['organization']['name'], ror_id: ror['organization']['id'] }
end

if in_file.blank?
  "Please put the path to the input file as the first argument"
  exit
end

csv = CSV.read(in_file, headers: true)
# remove all the random nils on the end of the table

# this seems to be all the meaningful and consistent columns in this type of csv
last_column = 39
fixed_headers = csv.headers[0..last_column]
new_headers = ['proposed_name', 'proposed_ror_id']

CSV.open(File.join(File.dirname(in_file), 'working_file_with_rors_added_by_name.csv'), "w") do |csv_out|
  csv_out << (fixed_headers + new_headers).flatten
  csv.each do |row|
    org_name = row['Parent Org Name']
    filled_ror = row['ROR and other mappings']
    org_info = {proposed: '', ror_id: ''}
    if org_name.present? && org_name != '#N/A' && ( filled_ror.blank? || filled_ror == '#N/A' )
      query = { affiliation: org_name }.to_query
      url = "https://api.ror.org/organizations?#{query}"
      puts "query #{org_name}"

      response = HTTP.get(url)
      org_info = find_best_result(response: response) if response.status == 200
      sleep 0.05
    end
    new_row = (row.to_a.map(&:second)[0..last_column] + [org_info[:proposed], org_info[:ror_id]]).flatten
    csv_out << new_row
  end
end


puts 'done'