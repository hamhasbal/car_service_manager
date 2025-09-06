# Car Service Manager

**Version:** 18.0.1.0.0 • **License:** LGPL-3

Car Service Manager is an Odoo module for tracking vehicle maintenance and repair orders.  It extends Odoo’s fleet management capabilities by letting you manage Cars (with owner/customer, brand, model, etc.), Mechanics, Service Types, and Service Orders.  Regular maintenance and repairs are critical to keep vehicles in good working order.  This module helps by logging each service or repair performed on a car, including the type of service, total cost, assigned mechanic, and any notes – essentially “logging every repair and maintenance performed” for each vehicle.  It integrates with Odoo Accounting to bill customers: when you confirm a service order, a customer invoice is automatically created (ensuring accurate billing and reduced admin work).  

## Features

- **Vehicle (Car) Management:**  Track each car’s **license plate**, owner (customer), brand, model, year, and next service due.  
- **Mechanics Management:**  Maintain a list of **Mechanics** with name, specialty, and contact.  
- **Service Types:**  Define different kinds of service (e.g. “Oil Change”, “Brake Inspection”), with a name, description, and price.  
- **Service Orders:**  Create **Service Orders** that link a Car, Service Type, and optionally a Mechanic.  
- **Order Workflow:**  Draft → Confirmed → Invoiced → Done / Cancelled.  
- **Automated Invoicing:**  On confirming a service order, a customer invoice is generated using Odoo’s accounting integration.  
- **Logging & Chatter:**  Service Orders inherit Odoo’s **Chatter** (messages, activities, and tracking).  
- **Reporting:**  A PDF report template for Service Orders is provided.  
- **Maintenance Scheduling:**  By keeping a history of past services and due dates, this module supports proactive maintenance scheduling.  

## Installation

1. Ensure Odoo 18.0 is installed.  
2. Install required modules: `base`, `mail`, and `om_account_accountant`.  
3. Copy **car_service_manager** into your Odoo addons directory.  
4. Update Apps list and install **Car Service Manager**.  

## Configuration

- Ensure an *Income* account exists in Accounting settings.  
- Configure access rights as needed.  
- A sequence for Service Orders (`car.service.order`) is auto-created.  

## Usage

1. Define **Service Types** with name, description, and price.  
2. Add **Mechanics** with name, specialty, and phone.  
3. Register **Cars** with license plate, owner (customer), brand, model, etc.  
4. Create **Service Orders** by selecting a Car and Service Type (customer auto-fills).  
5. Confirm an order → invoice is created automatically.  
6. Mark orders **Done** when completed.  
7. Cancel or reset to draft if needed (if invoice allows).  
8. Print Service Order reports as PDF.  

## Data Models

- **car.service (Car):** Vehicles with owner and details.  
- **car.mechanic:** Mechanics with specialty and contact.  
- **car.service.type:** Types of service with description and price.  
- **car.service.order:** Service Orders with workflow, invoices, and chatter.  

## Integration

- **Accounting:** Invoices created automatically and tracked in Odoo Accounting.  
- **Mail/Chatter:** Integrated with Odoo chatter.  
- **Fleet:** Complements Fleet by focusing on workshop/service orders.  

## License

This module is released under the GNU LGPLv3 license.  

## Contributing

Contributions and feedback are welcome. Open an issue or submit a pull request.  
